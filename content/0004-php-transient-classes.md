title: Learned this week
date: 2020-06-22
author: Harry
category: development
# PHP Transient Classes

    new class implements Interface{
        public function getId(): int {return $this->id;};
    }


# PHP Fat Arrow Functions

Since PHP 7.4.

    public function filterMandatory(): TaskList
    {
        return $this->filter(fn(Task $task) => $task->isMandatory());
    }

